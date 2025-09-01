# Dagster Integration Setup Guide

## Prerequisites
- **Meltano** and **dbt** projects already configured and working independently
- **Conda environment** with `dagster`, `dagster-dbt`, and `dbt-bigquery` installed

## Quick Start (Correct Sequence)

### Step 1: Create Dagster Scaffold
```bash
# Activate Dagster environment
conda activate dagster

# Create scaffold pointing to your dbt project
dagster-dbt project scaffold --project-name dagster_elt --dbt-project-dir ./austin_bikeshare_demo

cd dagster_elt
pip install -e .
```

### Step 2: Fix Generated Project Path
The scaffold generates incorrect paths. Fix `dagster_elt/dagster_elt/project.py`:

```python
from pathlib import Path
from dagster_dbt import DbtProject

# Remove the invalid packaged_project_dir parameter
austin_bikeshare_demo_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "austin_bikeshare_demo").resolve(),
)
austin_bikeshare_demo_project.prepare_if_dev()
```

### Step 3: Test Basic dbt Integration First
**IMPORTANT**: Test the dbt integration works before adding Meltano assets.

```bash
# Start Dagster (must include dbt parsing flag)
DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1 dagster dev

# Open UI and verify dbt assets appear
open http://localhost:3000
```

You should see dbt models (like `stg_trips`, `fact_trips`) in the asset graph.

### Step 4: Configure Core Files 
Only after dbt integration works, configure these three files:

#### File 1: `dagster_elt/dagster_elt/__init__.py`
```python
from .definitions import defs
```

#### File 2: `dagster_elt/dagster_elt/definitions.py`
**Replace the entire file** with:
```python
from dagster import Definitions
from dagster_dbt import DbtCliResource

# Import asset functions (will be created in next step)
from .assets import austin_bikeshare_demo_dbt_assets, meltano_extract_bikeshare_data
from .project import austin_bikeshare_demo_project 
from .schedules import schedules

defs = Definitions(
    # Register all asset functions
    assets=[
        austin_bikeshare_demo_dbt_assets,    # dbt models
        meltano_extract_bikeshare_data       # Meltano extraction
    ],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=austin_bikeshare_demo_project),
        # Note: No MeltanoResource needed (using subprocess approach)
    }
)
```

#### File 3: `dagster_elt/dagster_elt/assets.py`
**Replace the entire file** with:
```python
import subprocess
import os

from dagster import AssetExecutionContext, multi_asset, AssetOut, MaterializeResult, MetadataValue, AssetKey
from dagster_dbt import DbtCliResource, dbt_assets

from .project import austin_bikeshare_demo_project

# =============================================================================
# MELTANO EXTRACTION ASSETS
# =============================================================================

@multi_asset(
    outs={
        # Actual table names that Meltano loads
        "public_austin_bikeshare_trips": AssetOut(key_prefix=["bigquery_source"]),
        "public_austin_bikeshare_stations": AssetOut(key_prefix=["bigquery_source"])
    },
    description="Extract Austin bikeshare data from Postgres to BigQuery via Meltano",
    compute_kind="meltano"
)
def meltano_extract_bikeshare_data(context: AssetExecutionContext):
    """
    Multi-asset function that runs a single Meltano job to extract and load 2 tables.
    """
    
    # Path to Meltano project directory
    meltano_project_dir = os.path.join(os.path.dirname(__file__), "..", "..", "meltano-austin")
    
    # Execute Meltano job via subprocess
    result = subprocess.run(
        ["meltano", "run", "postgres-to-bigquery"],  # Actual job name
        cwd=meltano_project_dir,
        capture_output=True,
        text=True
    )
    
    # Log output for debugging
    context.log.info(f"Meltano stdout: {result.stdout}")
    if result.stderr:
        context.log.info(f"Meltano stderr: {result.stderr}")
    
    # Handle errors
    if result.returncode != 0:
        context.log.error(f"Meltano job failed with return code {result.returncode}")
        raise Exception("Meltano job failed. Check logs above for details.")
    
    # Return tuple of MaterializeResult (order matches outs definition)
    return (
        MaterializeResult(
            asset_key=AssetKey(['bigquery_source', 'public_austin_bikeshare_trips']),
            metadata={
                "meltano_job": MetadataValue.text("postgres-to-bigquery"),
                "table": MetadataValue.text("public_austin_bikeshare_trips"),
                "extraction_method": MetadataValue.text("meltano_subprocess")
            }
        ),
        MaterializeResult(
            asset_key=AssetKey(['bigquery_source', 'public_austin_bikeshare_stations']),
            metadata={
                "meltano_job": MetadataValue.text("postgres-to-bigquery"),
                "table": MetadataValue.text("public_austin_bikeshare_stations"), 
                "extraction_method": MetadataValue.text("meltano_subprocess")
            }
        )
    )

# =============================================================================
# DBT TRANSFORMATION ASSETS  
# =============================================================================

@dbt_assets(manifest=austin_bikeshare_demo_project.manifest_path)
def austin_bikeshare_demo_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """
    dbt assets that automatically discover models from austin_bikeshare_demo project.
    Creates dependencies: Meltano assets → dbt staging → dbt marts
    """
    yield from dbt.cli(["build"], context=context).stream()
```

### Step 5: Test Full Integration
```bash
# Restart Dagster to pick up new assets
DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1 dagster dev

# Test individual assets
dagster asset materialize --select "meltano_extract_bikeshare_data"
dagster asset materialize --select "austin_bikeshare_demo_dbt_assets"
```

## Critical Configuration Requirements

### Asset Key Matching
The integration requires **exact name coordination**:

#### Meltano Job Definition
```yaml
# meltano-austin/meltano.yml
jobs:
- name: postgres-to-bigquery  # Must match Dagster subprocess call
  tasks:
  - tap-postgres target-bigquery
```

#### Meltano Table Selection
```yaml
# meltano-austin/meltano.yml
extractors:
  - name: tap-postgres
    select:
    - public-austin_bikeshare_trips.*      # Must match Dagster asset name
    - public-austin_bikeshare_stations.*   # Must match Dagster asset name
```

#### dbt Source Configuration
```yaml
# austin_bikeshare_demo/models/sources.yml
sources:
  - name: bigquery_source              # Must match key_prefix in Dagster
    tables:
      - name: public_austin_bikeshare_trips     # Must match asset name in outs
      - name: public_austin_bikeshare_stations  # Must match asset name in outs
```

### Expected Asset Lineage
```
Meltano (Extract/Load)                           dbt (Transform)
├── public_austin_bikeshare_trips ────────────→ stg_trips ──→ fact_trips
└── public_austin_bikeshare_stations ─────────→ stg_stations ──→ dim_stations
```

## Troubleshooting Common Issues

### 1. "I don't see any assets"
**Problem**: No assets appear in Dagster UI
**Solutions**:
- Check `__init__.py` imports `defs`
- Verify `definitions.py` imports asset functions correctly
- Run `python -c "from dagster_elt import defs; print('Success')"`

### 2. "dbt assets work but no Meltano assets"
**Problem**: Only dbt models appear, no source tables
**Solutions**:
- Check import in `definitions.py`: `from .assets import meltano_extract_bikeshare_data`
- Verify asset function name matches import
- Check for Python syntax errors in `assets.py`

### 3. "MaterializeResult errors"
**Error**: `MaterializeResult did not include asset_key`
**Fix**: Each MaterializeResult needs explicit asset_key:
```python
MaterializeResult(
    asset_key=AssetKey(['bigquery_source', 'table_name']),
    metadata={...}
)
```

### 4. "Multi-asset return errors"
**Error**: `op has multiple outputs, but only one output was returned`
**Fix**: Return tuple, not dictionary:
```python
# Wrong
return {"table1": result1, "table2": result2}

# Correct  
return (result1, result2)
```

### 5. "No dependencies between assets"
**Problem**: Meltano and dbt assets run independently
**Solutions**:
- Verify `key_prefix=["bigquery_source"]` matches dbt source name
- Check asset names match table names in sources.yml exactly
- Ensure dbt sources.yml references the same tables Meltano loads

## Environment Setup

### Required Packages
```bash
conda activate dagster
pip install dagster dagster-webserver dagster-dbt dbt-bigquery
# Note: dagster-meltano NOT required with subprocess approach
```

### Development Commands
```bash
# Test asset discovery
dagster asset list

# Test definitions loading
cd dagster_elt
python -c "from dagster_elt import defs; print('Loaded successfully')"

# Run full pipeline
dagster asset materialize --select "*"
```

## File Structure Summary
```
project/
├── dagster_elt/                    # Orchestration (this guide)
│   ├── dagster_elt/
│   │   ├── __init__.py            # from .definitions import defs
│   │   ├── assets.py              # Multi-asset + dbt asset functions  
│   │   ├── definitions.py         # Central Dagster configuration
│   │   ├── project.py             # dbt project path (fix scaffold bugs)
│   │   └── schedules.py           # (generated, can be empty)
│   └── pyproject.toml             # (generated)
├── meltano-austin/                 # ELT (configured separately)
└── austin_bikeshare_demo/          # Transform (configured separately)
```

## Key Success Factors

1. **Follow the sequence**: Scaffold → Test dbt → Add Meltano → Test full integration
2. **Use exact names**: Asset names must match across Meltano, Dagster, and dbt
3. **Test incrementally**: Verify each step works before proceeding
4. **Fix scaffold bugs**: Remove invalid `packaged_project_dir` parameters
5. **Match import names**: Function names in assets.py must match imports in definitions.py

**Total setup time**: ~20 minutes | **Critical files**: 3 | **Key pattern**: Step-by-step validation
# EcoInventDownLoader (eidl)

The EcoInventDownLoader (eidl) is a small python package that automates the somewhat tedious process of adding an ecoinvent database to your python project. Without `eidl` the following steps are required: 

- Login to the ecoinvent homepage
- Choose and download the required database
- Unpack the 7z-archive on your computer (which will take up close to 2GB of disk space)
- Import the ecospold2 files with the `brightway2.SingleOutputEcospoldImporter`

With `eidl`, the above steps can all be carried out with a single command from a jupyter notebook or any python shell:
```
eidl.get_ecoinvent()
```
You will be asked to enter your ecoinvent username and password, and which version and system model you require. The database will then be added to your brightway2 project. Download and extraction are carried out in the background in a temporary directory, which is cleared after the import and therefore doesn't use up your disk space.

## Prerequisites

- Valid [ecoinvent](https://www.ecoinvent.org) login credentials
- [7-Zip file archiver](https://www.7-zip.org/) (installation instructions below)

## Installation

- Add the required conda channels to your conda config file, if you haven't done so already (ie. for the installation of brightway2):
```
conda config --append channels conda-forge
conda config --append channels cmutel
conda config --append channels haasad
```
- Simply install with conda:
```
conda install eidl
```
- ___Alternatively___ you can install `eidl` without adding the channels permanently:
```
conda install -c defaults -c conda-forge -c cmutel -c haasad eidl
```

## Example Usage

```python
import eidl
import brightway2 as bw
```

```python
bw.projects.set_current('eidl_demo')
```

```python
bw.bw2setup()
```

>    Creating default biosphere
>    
>
>
>    Writing activities to SQLite3 database:
>    0%                          100%
>    [##########                    ] | ETA: 00:00:00
>
>    Applying strategy: normalize_units
>    Applying strategy: drop_unspecified_subcategories
>    Applied 2 strategies in 0.00 seconds
>
>
>    [##############################] | ETA: 00:00:00
>    Total time elapsed: 00:00:00
>
>
>    Title: Writing activities to SQLite3 database:
>      Started: 04/25/2018 14:28:19
>      Finished: 04/25/2018 14:28:19
>      Total time elapsed: 00:00:00
>      CPU %: 63.10
>      Memory %: 0.93
>    Created database: biosphere3
>    Creating default LCIA methods
>    
>    Applying strategy: normalize_units
>    Applying strategy: set_biosphere_type
>    Applying strategy: drop_unspecified_subcategories
>    Applying strategy: link_iterable_by_fields
>    Applied 4 strategies in 0.98 seconds
>    Wrote 718 LCIA methods with 178008 characterization factors
>    Creating core data migrations

```python
eidl.get_ecoinvent()
```

>    ecoinvent username: user
>    ecoinvent password: ·············
>    logging in to ecoinvent homepage...
>    login successful!
>    
>     available versions:
>    a 3.4
>    b 3.3
>    c 3.2
>    d 3.1
>    e 3.01
>    version: a
>    
>     system models:
>    a apos
>    b consequential
>    c cutoff
>    system model: c
>    downloading cutoff 3.4 ...
>    download finished!: /tmp/tmpk4ripmd7/cutoff34.7z
>    
>    patool: Extracting /tmp/tmpk4ripmd7/cutoff34.7z ...
>    patool: running /usr/bin/7z x -o/tmp/tmpk4ripmd7 -- /tmp/tmpk4ripmd7/cutoff34.7z
>    patool: ... /tmp/tmpk4ripmd7/cutoff34.7z extracted to `/tmp/tmpk4ripmd7'.
>    Extracting XML data from 14889 datasets
>    Extracted 14889 datasets in 13.80 seconds
>    Applying strategy: normalize_units
>    Applying strategy: remove_zero_amount_coproducts
>    Applying strategy: remove_zero_amount_inputs_with_no_activity
>    Applying strategy: remove_unnamed_parameters
>    Applying strategy: es2_assign_only_product_with_amount_as_reference_product
>    Applying strategy: assign_single_product_as_activity
>    Applying strategy: create_composite_code
>    Applying strategy: drop_unspecified_subcategories
>    Applying strategy: fix_ecoinvent_flows_pre34
>    Applying strategy: link_biosphere_by_flow_uuid
>    Applying strategy: link_internal_technosphere_by_composite_code
>    Applying strategy: delete_exchanges_missing_activity
>    Applying strategy: delete_ghost_exchanges
>    Applying strategy: remove_uncertainty_from_negative_loss_exchanges
>    Applying strategy: fix_unreasonably_high_lognormal_uncertainties
>    Applying strategy: set_lognormal_loc_value
>    Applied 16 strategies in 4.56 seconds
>    14889 datasets
>    520205 exchanges
>    0 unlinked exchanges
>      
>    
>    Write database cutoff34 in project eidl_demo?
>    [y]/n y
>
>
>    Writing activities to SQLite3 database:
>    0%                          100%
>    [##############################] | ETA: 00:00:00
>    Total time elapsed: 00:01:22
>
>
>    Title: Writing activities to SQLite3 database:
>      Started: 04/25/2018 14:33:09
>      Finished: 04/25/2018 14:34:32
>      Total time elapsed: 00:01:22
>      CPU %: 56.10
>      Memory %: 7.07
>    Created database: cutoff34

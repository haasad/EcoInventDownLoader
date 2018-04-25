# EcoInventDownLoader (eidl)

> Download, unpack and import an ecoinvent database into your brightway2 project in one simple step.

The EcoInventDownLoader (eidl) is a small python package that automates the somewhat tedious process of adding an ecoinvent database to your python project. Without `eidl` the following steps are required: 

- Login to the ecoinvent homepage
- Choose and download the required database
- Unpack the 7z-archive on your computer (which will take up close to 2GB of disk space)
- Import the ecospold2 files with the `brightway2.SingleOutputEcospoldImporter`

With `eidl`, the above steps can all be carried out with a single command from a jupyter notebook or any python shell:
```
eidl.get_ecoinvent()
```
You will be asked to enter your ecoinvent username and password and which version and system model you require. The database will then be added to your brightway2 project. Download and extraction are carried out in the background in a temporary directory, which is cleared after the import and therefore doesn't use up your disk space.



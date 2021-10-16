[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stactools-packages/hwsd/main?filepath=docs/installation_and_basic_usage.ipynb)

# stactools-hwsd

- Name: hwsd
- Package: `stactools.hwsd`
- PyPI: https://pypi.org/project/stactools-hwsd/
- Owner: @jamesvrt
- Dataset homepage: http://example.com
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
  - [scientific](https://github.com/stac-extensions/scientific/)
  - [item-assets](https://github.com/stac-extensions/item-assets/)
  - [raster](https://github.com/stac-extensions/raster/)

A short description of the package and its usage.

## Examples

### STAC objects

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

### Command-line usage

Description of the command line functions

```bash
$ stac hwsd create-item -s source -d destination

$ stac hwsd create-collection -d destination

$ stac hwsd populate-collection -s source -d destination
```

Use `stac hwsd --help` to see all subcommands and options.

## Sync Customizations

Automatically sync Custom Fields and Property Setters in Frappe sites


### Usage

#### Exporting Customizations

Create Custom Fields and Property Setters as usual through Customize Form / Form Builder / respective DocTypes. The corresponding files should get auto-created in the following directory:

```
[bench-name]/sites/[site-name]/customizations/
```


#### Importing Customizations

Ensure that this app is installed and the `sites/[site-name]/customizations` directory is present. Customizations should get synced automatically during DB migration.

### License

MIT

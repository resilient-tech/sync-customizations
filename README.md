## Sync Customizations

Automatically sync Custom Fields and Property Setters in Frappe sites


### Usage

#### Exporting Customizations

Create Custom Fields and Property Setters as usual through Customize Form / Form Builder / respective DocTypes. The corresponding files should get auto-created in the following directory by default:

```
[bench-name]/sites/[site-name]/customizations/
```

You can also specify a custom directory for syncing customizations by setting the path to that directory in a site config called `customizations_dir`. This path must be either absolute or relative to the site's bench directory. For example:

```bash
bench --site abc.localhost set-config customizations_dir apps/abc/customizations
```


#### Importing Customizations

Ensure that this app is installed and the customizations directory is present. Customizations should get synced automatically during DB migration.

### License

MIT

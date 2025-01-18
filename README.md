## Run the app
Create or update an application package in your Snowflake account, upload application artifacts to a stage in the application package, and create or update an application object in the same account based on the uploaded artifacts.
```
snow app run
```

For more information, please refer to the Snowflake Documentation on installing and using Snowflake CLI to create a Snowflake Native App.  
# Directory Structure
## `/app`
This directory holds your Snowflake Native App files.

### `/app/README.md`
Exposed to the account installing the application with details on what it does and how to use it.

### `/app/manifest.yml`
Defines properties required by the application package. Find more details at the [Manifest Documentation.](https://docs.snowflake.com/en/developer-guide/native-apps/creating-manifest)

### `/app/setup_script.sql`
Contains SQL statements that are run when a consumer installs or upgrades a Snowflake Native App in their account.

## `/scripts`
You can add any additional scripts such as `.sql` and `.jinja` files here. One common use case for such a script is to add shared content from external databases to your application package. This allows you to refer to the external database in the setup script that runs when a Snowflake Native App is installed.
_Note: As of now, `snow app init` does not render these jinja templates for you into the required files, if you decide to use them. You will have to manually render them for now._


## `/src`
This directory contains code organization by functionality, such as one distinct module for Streamlit related code, another module for loading data from stage functionality,a and another modules for stored procedures which generates recommendations. template. 

## `snowflake.yml.jinja`
While this file exists as a Jinja template, it is the only file that is automatically rendered as a `snowflake.yml` file by the `snow app init` command, as described in the [README.md](../README.md). Snowflake CLI uses the `snowflake.yml` file  to discover your project's code and interact with Snowflake using all relevant privileges and grants. 

For more information, please refer to the Snowflake Documentation on installing and using Snowflake CLI to create a Snowflake Native App. 

## Adding a snowflake.local.yml file
Although your project directory must have a `snowflake.yml` file, an individual developer can choose to customize the behavior of Snowflake CLI by providing local overrides to the `snowflake.yml` file, such as a new role to test out your own application package. This is where you can use the `snowflake.local.yml` file, which is not a version-controlled file.

For more information, please refer to the Snowflake Documentation on installing and using Snowflake CLI to create a Snowflake Native App. 
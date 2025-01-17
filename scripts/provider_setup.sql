---- Create a view in the appllication package from the another database. This view needs to be shared as a part of the application
USE APPLICATION PACKAGE <% ctx.entities.app_pkg.identifier %>;

CREATE SCHEMA IF NOT EXISTS shared_content;

CREATE VIEW IF NOT EXISTS app_pkg.shared_content.view_created_frm_data
AS SELECT *
FROM SUPP_ANALYTICS_DB.DATA.DIM_TAXONOMY_CODE;

GRANT REFERENCE_USAGE ON DATABASE SUPP_ANALYTICS_DB  TO SHARE IN APPLICATION PACKAGE <% ctx.entities.app_pkg.identifier %>;

GRANT USAGE ON SCHEMA app_pkg.shared_content TO SHARE IN APPLICATION PACKAGE <% ctx.entities.app_pkg.identifier %>;

GRANT SELECT ON VIEW app_pkg.shared_content.view_created_frm_data TO SHARE IN APPLICATION PACKAGE <% ctx.entities.app_pkg.identifier %>;

CREATE VIEW IF NOT EXISTS app_pkg.shared_content.view_created_frm_spend
AS SELECT *
FROM SUPP_ANALYTICS_DB.DATA.FACT_SUPP_ANALYTICS_SPEND_TRANSACTION;

GRANT SELECT ON VIEW app_pkg.shared_content.view_created_frm_spend  TO SHARE IN APPLICATION PACKAGE <% ctx.entities.app_pkg.identifier %>;

----------------------------

CREATE VIEW IF NOT EXISTS app_pkg.shared_content.view_created_from_faqs
AS SELECT *
FROM SUPP_ANALYTICS_DB.DATA.FAQS_DATA;

GRANT SELECT ON VIEW app_pkg.shared_content.view_created_from_faqs  TO SHARE IN APPLICATION PACKAGE <% ctx.entities.app_pkg.identifier %>;


CREATE OR ALTER VERSIONED SCHEMA core;

CREATE APPLICATION ROLE IF NOT EXISTS app_public;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;

------ CREATE A VIEW FROM ANOTHER DATABASE WITHIN THE APPLICATION PACKAGE AND SHARE WITHIN THE APPLICATION

create view if not exists core.view_frm_pkg
as select *
from app_pkg.shared_content.view_created_frm_data;

grant select on view core.view_frm_pkg to application role app_public;

--------------

create view if not exists core.view_frm_spend_pkg
as select *
from app_pkg.shared_content.view_created_frm_spend;

grant select on view core.view_frm_spend_pkg to application role app_public;

-------------------------------------------------------------------------------------

CREATE STREAMLIT IF NOT EXISTS core.SUPPLIER_ANALYTICS
  FROM '/streamlit'
  MAIN_FILE = '/1_Summary.py'
;

GRANT USAGE ON STREAMLIT core.SUPPLIER_ANALYTICS TO APPLICATION ROLE app_public;

--------------------------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS APP_DATA;
GRANT USAGE ON SCHEMA APP_DATA TO APPLICATION ROLE APP_PUBLIC;

CREATE OR REPLACE  VIEW  app_data.DIM_TAXONOMY_CODE             --VIEW_FROM_PKG1
AS SELECT * FROM app_pkg.shared_content.view_created_frm_data;

grant all PRIVILEGES on view app_data.DIM_TAXONOMY_CODE to application role app_public;
grant select on view app_data.DIM_TAXONOMY_CODE to application role app_public;


------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW  app_data.FACT_SUPP_ANALYTICS_SPEND_TRANSACTION

AS SELECT * FROM app_pkg.shared_content.view_created_frm_spend;

grant all PRIVILEGES on view app_data.FACT_SUPP_ANALYTICS_SPEND_TRANSACTION
  to application role app_public;

grant select on view app_data.FACT_SUPP_ANALYTICS_SPEND_TRANSACTION
 to application role app_public;

-----------------------------

CREATE SCHEMA IF NOT EXISTS FAQS_sh;

GRANT USAGE ON SCHEMA FAQS_sh TO APPLICATION ROLE APP_PUBLIC;

CREATE VIEW if not exists FAQS_sh.view_from_faq
AS SELECT * FROM app_pkg.shared_content.view_created_from_faqs;


grant all PRIVILEGES on view FAQS_sh.view_from_faq to application role app_public;

grant select on view FAQS_sh.view_from_faq to application role app_public;
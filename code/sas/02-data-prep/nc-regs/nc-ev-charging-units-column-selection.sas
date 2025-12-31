/*==============================================================
  SAS Curiosity Cup 2026 — AFDC Charging Units Curation (KEEP-only)
  Input : CUPDATA.EV_CHARGING_UNITS
  Output: CUPDATA.NC_EV_CHARGING_UNITS

  Enforced:
    - No joins
    - No filtering (row counts must match)
    - No feature engineering / cleaning / standardizing values
    - Exact KEEP list, exact order
    - Fail-fast if missing columns (with available columns listing)
==============================================================*/

options mprint mlogic symbolgen;
options validvarname=any;

/*-----------------------------
  1) Configuration
-----------------------------*/
%let IN_LIB  = CUPDATA;
%let IN_TBL  = EV_CHARGING_UNITS;

%let OUT_LIB = CUPDATA;
%let OUT_TBL = NC_EV_CHARGING_UNITS;

/*-----------------------------
  2) Logging + utilities
-----------------------------*/
%macro log_info(msg);  %put NOTE: [INFO] &msg; %mend;
%macro log_error(msg); %put ERROR: [ERROR] &msg; %mend;

%macro fail_fast(msg);
  %log_error(&msg);
  %abort cancel;
%mend;

%macro assert_table_exists(lib, mem);
  %local dsid rc;
  %let dsid = %sysfunc(open(&lib..&mem, i));
  %if &dsid = 0 %then %do;
    %fail_fast(Table not found: &lib..&mem. Ensure the input table exists before running this program.);
  %end;
  %let rc = %sysfunc(close(&dsid));
%mend;

/* Conservative normalization for matching:
   - trim
   - collapse whitespace
   - underscore -> space
   - lower
*/
%macro norm(col);
  lowcase(compbl(tranwrd(strip(&col), '_', ' ')))
%mend;

/*-----------------------------
  3) Pre-flight
-----------------------------*/
%assert_table_exists(&IN_LIB, &IN_TBL);
%log_info(Input table exists: &IN_LIB..&IN_TBL);

/*-----------------------------
  4) KEEP contract (authoritative order)
-----------------------------*/
data work._keep_contract;
  length desired $256 desired_norm $256 order 8;
  infile datalines truncover;
  input desired $char256.;
  desired = strip(desired);
  if desired = "" then delete;
  desired_norm = %norm(desired);
  order + 1;
  datalines;
ID
Station Name
Latitude
Longitude
City
State
ZIP
EV DC Fast Count
EV Level2 EVSE Num
EV Level1 EVSE Num
EV CCS Connector Count
EV CHAdeMO Connector Count
EV J1772 Connector Count
EV J3400 Connector Count
EV Connector Types
Access Code
Status Code
Geocode Status
Restricted Access
Open Date
Date Last Confirmed
Updated At
EV Network
Facility Type
Owner Type Code
;
run;

/* Input column inventory */
proc sql noprint;
  create table work._input_cols as
  select
    varnum,
    name as in_name length=128,
    %norm(name) as in_norm length=256
  from dictionary.columns
  where libname = upcase("&IN_LIB")
    and memname = upcase("&IN_TBL")
  order by varnum;
quit;

/*-----------------------------
  5) Detect normalization collisions (ambiguous schema)
-----------------------------*/
proc sql noprint;
  create table work._collisions as
  select in_norm, count(*) as n
  from work._input_cols
  group by in_norm
  having calculated n > 1;

  select count(*) into :NCOLL trimmed from work._collisions;
quit;

%macro assert_no_collisions;
  %if %sysevalf(&NCOLL > 0) %then %do;
    %log_error(Ambiguous schema: multiple input columns normalize to the same key. Cannot proceed safely.);
    %log_error(Collision groups:);
    proc sql;
      select c.in_norm, i.varnum, i.in_name
      from work._collisions c
      inner join work._input_cols i
        on c.in_norm = i.in_norm
      order by c.in_norm, i.varnum;
    quit;
    %fail_fast(Resolve collisions by renaming one of the colliding input columns, then rerun.);
  %end;
%mend;

%assert_no_collisions;

/*-----------------------------
  6) Map KEEP contract -> input columns; fail-fast if missing
-----------------------------*/
proc sql noprint;
  create table work._schema_map as
  select
    k.order,
    k.desired,
    i.in_name
  from work._keep_contract k
  left join work._input_cols i
    on k.desired_norm = i.in_norm
  order by k.order;

  create table work._missing as
  select order, desired
  from work._schema_map
  where missing(in_name)
  order by order;

  select count(*) into :NMISSING trimmed from work._missing;
quit;

%macro assert_no_missing;
  %if %sysevalf(&NMISSING > 0) %then %do;
    %log_error(FAIL-FAST: One or more KEEP columns are missing from &IN_LIB..&IN_TBL..);
    %log_error(Missing KEEP columns:);
    data _null_;
      set work._missing;
      put "ERROR:   - " desired;
    run;

    %log_error(Available input columns detected in &IN_LIB..&IN_TBL:);
    data _null_;
      set work._input_cols;
      put "ERROR:   - " in_name;
    run;

    %abort cancel;
  %end;
%mend;

%assert_no_missing;

/* Audit: mapping */
%log_info(KEEP_LIST -> Input column mapping:);
data _null_;
  set work._schema_map;
  put "NOTE: [MAP] " desired " <= " in_name;
run;

/*-----------------------------
  7) Row counts (pre)
-----------------------------*/
proc sql noprint;
  select count(*) into :IN_ROWS trimmed from &IN_LIB..&IN_TBL;
quit;

%log_info(Input row count = &IN_ROWS);

/*-----------------------------
  8) Build ordered lists for RETAIN (desired) and SET KEEP (actual)
-----------------------------*/
%let RETAIN_LIST=;
%let SET_KEEP_LIST=;

data _null_;
  set work._schema_map;
  length retain_piece keep_piece $400;

  retain_piece = catt('"', strip(desired), '"n');
  keep_piece   = catt('"', strip(in_name), '"n');

  call symputx('RETAIN_LIST', catx(' ', symget('RETAIN_LIST'), retain_piece), 'G');
  call symputx('SET_KEEP_LIST', catx(' ', symget('SET_KEEP_LIST'), keep_piece), 'G');
run;

/*-----------------------------
  9) Create output table (projection only; no transformations)
-----------------------------*/
data &OUT_LIB..&OUT_TBL;
  retain &RETAIN_LIST;
  set &IN_LIB..&IN_TBL (keep=&SET_KEEP_LIST);
run;

/*-----------------------------
 10) Row integrity check (post)
-----------------------------*/
proc sql noprint;
  select count(*) into :OUT_ROWS trimmed from &OUT_LIB..&OUT_TBL;
quit;

%log_info(Output row count = &OUT_ROWS);

%macro assert_row_counts_match;
  %if %sysevalf(%sysfunc(inputn(&IN_ROWS,best.)) ne %sysfunc(inputn(&OUT_ROWS,best.))) %then %do;
    %fail_fast(Row count mismatch: input=&IN_ROWS output=&OUT_ROWS. Filtering occurred unexpectedly.);
  %end;
%mend;

%assert_row_counts_match;

/*-----------------------------
 11) Required audit outputs
-----------------------------*/
title "Row Count Check: &IN_LIB..&IN_TBL vs &OUT_LIB..&OUT_TBL";
proc sql;
  select
    (select count(*) from &IN_LIB..&IN_TBL)   as input_rows,
    (select count(*) from &OUT_LIB..&OUT_TBL) as output_rows
  ;
quit;
title;

title "Ordered Output Column List: &OUT_LIB..&OUT_TBL";
proc sql;
  select varnum, name
  from dictionary.columns
  where libname = upcase("&OUT_LIB")
    and memname = upcase("&OUT_TBL")
  order by varnum;
quit;
title;

%log_info(SUCCESS: Created &OUT_LIB..&OUT_TBL with KEEP-only schema and matched row counts.);

/*-----------------------------
 12) Optional cleanup
-----------------------------*/
proc datasets lib=work nolist;
  delete _keep_contract _input_cols _collisions _schema_map _missing;
quit;

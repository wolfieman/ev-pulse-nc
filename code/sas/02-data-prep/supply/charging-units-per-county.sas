/* FINAL FIX: create the authoritative charger + county table */
proc sql;
  create table cupdata.nc_ev_charging_units_county as
  select
    a.*,
    b.name as County_Name_from_lookup length=100
  from cupdata.nc_ev_charging_units_county as a
  left join cupdata.nc_county_lookup_norm as b
    on put(input(compress(a.County_GEOID,,'kd'), best.), z5.) = b.geoid_norm
  ;
quit;

/* Overwrite County_Name safely */
data cupdata.nc_ev_charging_units_county;
  set cupdata.nc_ev_charging_units_county;
  County_Name = County_Name_from_lookup;
  drop County_Name_from_lookup;
run;

proc sql;
  select
    count(*) as total_rows,
    sum(missing(County_Name)) as missing_county_name,
    calculated missing_county_name / calculated total_rows as pct_missing format=percent8.2
  from cupdata.nc_ev_charging_units_county;
quit;

proc freq data=cupdata.nc_ev_charging_units_county;
  tables County_Name / missing;
run;


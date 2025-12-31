proc sql;
  create table cupdata.nc_county_charger_supply as
  select
    County_GEOID,
    County_Name,
    count(*) as chargers
  from cupdata.nc_ev_charging_units_county
  group by County_GEOID, County_Name;
quit;

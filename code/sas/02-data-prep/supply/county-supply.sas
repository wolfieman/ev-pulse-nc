/* S7_BUILD_COUNTY_SUPPLY.sas
   Input : CUPDATA.NC_EV_CHARGING_UNITS_COUNTY
   Output: CUPDATA.NC_COUNTY_CHARGER_SUPPLY
*/

proc sql;
  create table cupdata.nc_county_charger_supply as
  select
    County_GEOID,
    County_Name,
    count(*) as chargers
  from cupdata.nc_ev_charging_units_county
  group by County_GEOID, County_Name
  order by chargers desc;
quit;

/* QA */
proc sql;
  select count(*) as counties_with_chargers
  from cupdata.nc_county_charger_supply;
quit;

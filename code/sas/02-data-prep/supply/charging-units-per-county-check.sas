proc sql;
  select count(distinct County_GEOID) as distinct_counties
  from cupdata.nc_ev_charging_units_county;
quit;

proc sql;
  select County_Name, count(*) as chargers
  from cupdata.nc_ev_charging_units_county
  group by County_Name
  order by chargers desc;
quit;

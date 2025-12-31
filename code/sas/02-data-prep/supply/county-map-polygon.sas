/* Authoritative NC county polygon layer */
data cupdata.nc_county_polygons
     (keep=x y segment geoid statefp countyfp name);
  set work.us_counties;
  where statefp = '37';
run;

/* Optional but safe: ensure sorted for spatial procedures */
proc sort data=cupdata.nc_county_polygons;
  by geoid segment;
run;

/* Expect 100 counties */
proc sql;
  select count(distinct geoid) as nc_counties
  from cupdata.nc_county_polygons;
quit;

/* Confirm geometry still exists */
proc contents data=cupdata.nc_county_polygons;
run;


/* NC-only polygons in CUPDATA (keeps only what we need) */
data cupdata.nc_counties_map (keep=x y segment geoid statefp countyfp name);
  set work.us_counties;
  where statefp = '37';
run;


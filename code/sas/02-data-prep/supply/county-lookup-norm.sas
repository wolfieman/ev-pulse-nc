/* S4_BUILD_NC_COUNTY_LOOKUP_NORM.sas
   Input : CUPDATA.NC_COUNTY_POLYGONS
   Output: CUPDATA.NC_COUNTY_LOOKUP_NORM
*/

data cupdata.nc_county_lookup_norm;
  set cupdata.nc_county_polygons(keep=geoid name);
  length geoid_norm $5;
  geoid_norm = put(input(compress(geoid,,'kd'), best.), z5.);
  keep geoid_norm name;
run;

proc sort data=cupdata.nc_county_lookup_norm nodupkey;
  by geoid_norm;
run;

/* QA */
proc sql;
  select count(*) as rows, count(distinct geoid_norm) as distinct_geoid
  from cupdata.nc_county_lookup_norm;
quit;

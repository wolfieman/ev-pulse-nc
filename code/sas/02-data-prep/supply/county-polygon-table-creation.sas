/* S3_BUILD_NC_COUNTY_POLYGONS.sas
   Input : TIGER county shapefile components on disk (.shp/.dbf/.shx/.prj)
   Output: CUPDATA.NC_COUNTY_POLYGONS (NC only)
*/

%let shp_dir=/export/viya/homes/wsanyer@broncos.uncfsu.edu/wolfie/curiosity-cup/shapefiles;
%let shp=tl_2025_us_county.shp;

/* 1) Import the county shapefile */
proc mapimport
  datafile="&shp_dir/&shp"
  out=work.us_counties_raw;
run;

/* 2) Filter to North Carolina only (STATEFP='37') */
data cupdata.nc_county_polygons;
  set work.us_counties_raw;
  where statefp='37';
run;

/* 3) Sort for spatial procedures */
proc sort data=cupdata.nc_county_polygons;
  by geoid segment;
run;

/* 4) QA: Expect 100 counties */
proc sql;
  select count(distinct geoid) as nc_counties
  from cupdata.nc_county_polygons;
quit;

/* S5_SPATIAL_JOIN_CHARGERS_TO_COUNTY_GEOID.sas
   Input : CUPDATA.NC_EV_CHARGING_UNITS (points via lat/lon)
           CUPDATA.NC_COUNTY_POLYGONS   (polygons)
   Output: CUPDATA.NC_EV_CHARGING_UNITS_COUNTY (adds County_GEOID)
*/

data work.chargers_pts(keep=point_id x y);
  set cupdata.nc_ev_charging_units;
  point_id=_n_;
  x=Longitude;   /* X=lon */
  y=Latitude;    /* Y=lat */
run;

proc sort data=work.chargers_pts;
  by point_id;
run;

proc ginside
  data=work.chargers_pts
  map=cupdata.nc_county_polygons
  out=work.chargers_in_county;
  id geoid;
run;

/* Merge County_GEOID back to chargers using point_id */
data cupdata.nc_ev_charging_units_county;
  merge cupdata.nc_ev_charging_units(in=a)
        work.chargers_in_county(keep=point_id geoid rename=(geoid=County_GEOID));
  point_id=_n_;
  if a;
  drop point_id;
run;

/* QA */
proc sql;
  select
    count(*) as total_rows,
    sum(missing(County_GEOID)) as unassigned_rows
  from cupdata.nc_ev_charging_units_county;
quit;

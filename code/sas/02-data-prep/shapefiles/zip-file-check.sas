/*------------------------------------------------------------*/
/* CONFIG                                                     */
/*------------------------------------------------------------*/
%let shpdir=/export/viya/homes/wsanyer@broncos.uncfsu.edu/wolfie/curiosity-cup/shapefiles;
%let zipfile=&shpdir./tl_2025_us_county.zip;
%let shpname=tl_2025_us_county.shp;
%let outshp=&shpdir./&shpname;

/*------------------------------------------------------------*/
/* STEP 1: Confirm the ZIP contains the .shp member            */
/*------------------------------------------------------------*/
filename zref zip "&zipfile";

data work.zip_members;
  length memname $256;
  fid = dopen("zref");
  if fid = 0 then do;
    putlog "ERROR: Cannot open ZIP: &zipfile";
    stop;
  end;

  n = dnum(fid);
  do i = 1 to n;
    memname = dread(fid, i);
    output;
  end;

  rc = dclose(fid);
  drop fid n i rc;
run;

proc print data=work.zip_members noobs;
  title "Members inside &zipfile";
run;

/*------------------------------------------------------------*/
/* STEP 2: Extract the .shp from the ZIP (binary-safe)         */
/*------------------------------------------------------------*/
data _null_;
  length _msg $300;

  /* Read the shapefile bytes from the ZIP member */
  infile zref("&shpname") recfm=n lrecl=32767 end=eof;

  /* Write bytes to the destination path */
  file "&outshp" recfm=n lrecl=32767;

  input;
  put _infile_;

  if eof then do;
    _msg = cats("NOTE: Extracted ", "&shpname", " to ", "&outshp");
    putlog _msg;
  end;
run;

filename zref clear;

/*------------------------------------------------------------*/
/* STEP 3: Verify the .shp now exists (directory listing)      */
/*------------------------------------------------------------*/
filename dirref "&shpdir";

data _null_;
  did = dopen('dirref');
  if did = 0 then do;
    putlog "ERROR: Cannot open directory: &shpdir";
    stop;
  end;

  found = 0;
  do i=1 to dnum(did);
    fname = dread(did,i);
    if lowcase(fname) = lowcase("&shpname") then found = 1;
  end;

  rc = dclose(did);

  if found then putlog "NOTE: Confirmed .shp exists on disk: &outshp";
  else putlog "ERROR: .shp not found after extraction: &outshp";
run;

/*------------------------------------------------------------*/
/* STEP 4: Import shapefile from disk (now full set exists)    */
/*------------------------------------------------------------*/
proc mapimport
  datafile="&outshp"
  out=work.us_counties;
run;

/*------------------------------------------------------------*/
/* STEP 5: Validate                                            */
/*------------------------------------------------------------*/
proc sql;
  select count(*) as obs from work.us_counties;
quit;

proc contents data=work.us_counties;
run;

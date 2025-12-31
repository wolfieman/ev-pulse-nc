/* Create a new CAS table with a valid date column */
data casuser.NC_EV_PHEV_TS;
    set casuser.NC_EV_PHEV_MONTHLY_MASTER;

    /* Convert the character Month field (YYYY-MM) to a true SAS date */
    MonthDate = input(cats(Month, '-01'), yymmdd10.);

    /* Optional: assign a date display format for clarity */
    format MonthDate yymmn6.;

    /* Keep useful columns; reorder if needed */
    keep Month MonthDate County Electric PlugInHybrid;
run;

/* Promote and save the table so it appears in Data Explorer */
proc casutil;
    promote casdata="NC_EV_PHEV_TS" incaslib="casuser" outcaslib="casuser";
    save casdata="NC_EV_PHEV_TS" casout="NC_EV_PHEV_TS.sashdat" replace;
quit;
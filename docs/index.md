# Notes

- Veer in docker-compose we are using a postgis image
- Note especially the mounting dir =  postgres_data:/var/lib/postgresql/
- instead of  postgres_data:/var/lib/postgresql/data which we do normally
- somehow this postgis image thing or postgres version thing I am not sure

- Note in docker file we run a command to install GDAL as well so the geodjango
- can find it in the main django container
- GDAL is not expected in the the postgis container!

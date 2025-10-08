# Database
PostgreSQL was chosen for its flexibility with data structures.


## Steps used to setup
1. SSH into Raspberry Pi: `ssh pi3@<ip_address | mqtt.io>`
2. Install PostgreSQL: `sudo apt install postgresql -y`
3. Switch to postgres user: `sudo su postgres`
4. Go to postgres user home: `cd ~`
5. Create a new user: `createuser <USERNAME> -P --interactive` (prompts for password and accept superuser to be able to create databases)
6. Create a new database: `createdb <DBNAME> -O <USERNAME>`
7. Access psql shell: `psql`
8. List databases: `\l`
9. Connect to database: `\c <DBNAME>`
10. List users: `\du`
11. Create a new table: `CREATE TABLE device_history ( id BIGSERIAL PRIMARY KEY, device_id INT NOT NULL, recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(), data JSONB NOT NULL);`
12. List tables: `\dt`
13. Expose port 5432 in firewall: `sudo ufw allow 5432/tcp`

### Optional to allow remote connections
- expose port `vim /etc/postgresql/15/main/pg_hba.conf` and add CIDR block for IPv4
- change listen address `vim /etc/postgresql/15/main/postgresql.conf` and change `listen_addresses = 'localhost'` to `listen_addresses = '*'`
- exit the su postgres user: `exit`
- restart PostgreSQL: `sudo systemctl restart postgresql`

## Steps to initalize Prisma







<!-- 9. Exit psql shell: `\q`
10. Exit postgres user: `exit`
11. Allow remote connections: `sudo nano /etc/postgresql/14/main/pg_hba.conf` and add `host    all             all             0.0.0.0/0               md5`
12. Allow listening on all IPs: `sudo nano /etc/postgresql/14/main/postgresql.conf` and change `listen_addresses = 'localhost'` to `listen_addresses = '*'`
13. Restart PostgreSQL: `sudo systemctl restart postgresql`
14. Test connection from local machine: `psql -h <ip_address | mqtt.io> -U <USERNAME> -d <DBNAME>` -->



## Sources
- [Pi PostgreSQL](https://pimylifeup.com/raspberry-pi-postgresql/)


### Steps for setup
1. `sudo apt update && sudo apt upgrade -y`
2. `sudo apt install -y nodejs npm`

3. `npm init --yes && npm set-script type module`
4. `npm install prisma typescript tsx @types/node --save-dev`
5. `npx tsc --init`
6. `npx prisma init --datasource-provider postgresql`


## Sources
- [Prisma setup](https://www.prisma.io/docs/getting-started/setup-prisma/start-from-scratch/relational-databases-typescript-prismaPostgres)
#!/usr/bin/env bash
#usage:xxx
#scripts_name:${NAME}.sh
# author：xiaojian
IP_info="127.0.0.1"

cd /usr/bin/
MongoDB="mongo mongodb://127.0.0.1:27017"
$MongoDB << EOF
rsconf={
        _id:"myset",
        members: [
            {_id: 0, host: "${IP_info}:27017"},
            {_id: 1, host: "${IP_info}:27018"},
            {_id: 2, host: "${IP_info}:27019"}
        ]
}

rs.initiate(rsconf)
exit;
EOF

sleep 8

MongoDB_cluster="mongo mongodb://127.0.0.1:27018,127.0.0.1:27019,127.0.0.1:27017/?replicaSet=myset"
$MongoDB_cluster <<EOF
use admin
 db.createUser(
   {
     user: "root",
     pwd: "Ft_Mongo_123",
     roles: [ { role: "root", db: "admin" } ]
   }
 )

exit;
EOF

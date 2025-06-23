aws_region     = "eu-west-2"
aws_access_key = "complete-this"
aws_secret_key = "complete-this"

app_name        = "spacex"
app_environment = "dev"

redshift_vpc_cidr      = "10.20.0.0/16"
redshift_subnet_1_cidr = "10.20.1.0/24"
redshift_subnet_2_cidr = "10.20.2.0/24"

redshift_cluster_identifier = "spacex-cluster"
redshift_database_name      = "spacexdb"
redshift_admin_username     = "alvaroadmin"
redshift_admin_password     = "passwordtochange"
redshift_node_type          = "dc2.large"
redshift_cluster_type       = "multi-node"
redshift_number_of_nodes    = 2
PROJECT_ID  := $(shell terraform output -raw project_id)
PROJECT_ID_SUFFIX := $(shell terraform output -raw project_id_suffix)
PROJECT_NR  := $(shell terraform output -raw project_nr)
ORG_ID      := $(shell terraform output -raw org_id)
FOLDER_ID_1 := $(shell terraform output -raw folder_id_1)
FOLDER_ID_2 := $(shell terraform output -raw folder_id_2)
CURL         = ../../bin/curl-wrap.sh
JSON_CLEANER = ../../bin/json-cleaner

ZONE_EMPTY   = europe-west4-b

FAKE_PROJECT_ID_SUFFIX = aaaa
FAKE_PROJECT_NR = 12340004
FAKE_ORG_ID = 11112222
FAKE_FOLDER_ID_1 = 100001
FAKE_FOLDER_ID_2 = 100002
SED_SUBST_FAKE = sed -e "s/$(PROJECT_ID_SUFFIX)/$(FAKE_PROJECT_ID_SUFFIX)/" \
		     -e "s/$(PROJECT_NR)/$(FAKE_PROJECT_NR)/" \
		     -e "s/$(ORG_ID)/$(FAKE_ORG_ID)/" \
		     -e "s/$(FOLDER_ID_1)/$(FAKE_FOLDER_ID_1)/" \
		     -e "s/$(FOLDER_ID_2)/$(FAKE_FOLDER_ID_2)/"

all:	\
	json-dumps/compute-instances-empty.json \
	json-dumps/compute-migs-empty.json \
	json-dumps/compute-network-default.json \
	json-dumps/compute-subnetworks-europe-west4.json \
	json-dumps/compute-effective-firewalls-default.json \
	json-dumps/compute-project.json \
	json-dumps/compute-zones.json \
	json-dumps/iam-policy.json \
	json-dumps/iam-roles-custom.json \
	json-dumps/iam-service-accounts.json \
	json-dumps/project.json \
	json-dumps/services.json

# compute.googleapis.com

json-dumps/compute-zones.json:
	$(CURL) -fsS \
		'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/zones' \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-instances-empty.json:
	$(CURL) -fsS \
		'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/zones/$(ZONE_EMPTY)/instances' \
		| $(JSON_CLEANER) instances \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-migs-empty.json:
	$(CURL) -fsS \
		'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/zones/$(ZONE_EMPTY)/instanceGroupManagers' \
		| $(JSON_CLEANER) instances \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-project.json:
	$(CURL) -fsS \
		'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)' \
		| $(JSON_CLEANER) compute-project \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-network-default.json:
	$(CURL) -fsS \
	        'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/global/networks/default' \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-subnetworks-%.json:
	REGION=$(subst json-dumps/,,$*); \
	$(CURL) -fsS \
	        "https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/regions/$$REGION/subnetworks" \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-effective-firewalls-default.json:
	$(CURL) -fsS \
	        'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/global/networks/default/getEffectiveFirewalls' \
		| $(SED_SUBST_FAKE) >$@


# cloudresourcemanager.googleapis.com

json-dumps/project.json:
	$(CURL) -fsS \
		'https://cloudresourcemanager.googleapis.com/v3/projects/$(PROJECT_ID)' \
		| $(SED_SUBST_FAKE) >$@

json-dumps/iam-policy.json:
	$(CURL) -fsS \
		'https://cloudresourcemanager.googleapis.com/v1/projects/$(PROJECT_ID):getIamPolicy' \
		-X POST  --header "Content-Type:text/json" \
		-d "" \
		| $(JSON_CLEANER) other \
		| $(SED_SUBST_FAKE) >$@

# iam.googleapis.com

json-dumps/iam-roles-custom.json:
	$(CURL) -fsS \
		'https://iam.googleapis.com/v1/projects/$(PROJECT_ID)/roles?view=FULL&pageSize=500' \
		| $(SED_SUBST_FAKE) >$@

json-dumps/iam-service-accounts.json:
	$(CURL) -fsS \
		'https://iam.googleapis.com/v1/projects/$(PROJECT_ID)/serviceAccounts' \
		| $(JSON_CLEANER) service-accounts \
		| $(SED_SUBST_FAKE) >$@

# serviceusage.googleapis.com

json-dumps/services.json:
	$(CURL) -fsS \
	        'https://serviceusage.googleapis.com/v1/projects/$(PROJECT_ID)/services?filter=state:ENABLED' \
		| $(SED_SUBST_FAKE) >$@

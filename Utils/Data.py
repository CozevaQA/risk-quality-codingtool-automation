import os
# Cozeva URLs and Credentials
prod_login_url = "https://www.cozeva.com/user/login"
prod_logout_url = "https://www.cozeva.com/user/logout"
prod_base_url = "https://www.cozeva.com/"
cert_login_url = "https://cert.cozeva.com/user/login"
cert_logout_url = "https://cert.cozeva.com/user/logout"
cert_base_url = "https://cert.cozeva.com/"
username = os.environ.get('CS2_User')
password = os.environ.get('CS2_Password')
reason_field = "https://redmine2.cozeva.com/issues/24376"
patient_cz_id = ""
note = ""
dx_code = ""
dos_field = ""
provider_name = ""
delete_reason = "CozevaQA"
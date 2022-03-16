RESOURCE_GROUP_NAME="artlink"
APP_SERVICE_NAME="artlink-linux-F1"

az webapp deploy ^
	--src-path "SsarThreeApi.zip" ^
--ids "/subscriptions/76a97cc0-67d4-45c8-8157-5b5d48ae769e/resourceGroups/appsvc_linux_centralus/providers/Microsoft.Web/sites/artlink-apservice"

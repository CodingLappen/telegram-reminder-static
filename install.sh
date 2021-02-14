FILES="bot.py Telegram.db"
INSTALL_PATH="/etc/telegram-reminder"
SERVICE_FILE="telegram-reminder.service"


if  [ ! $EUID=0 ] ; then
	echo "This script must be run as root"
	exit 1
fi

case $1 in
	install)
		mkdir -p $INSTALL_PATH
		python3 -m pip install setuptools setuptools_rust
		unzip python-telegram-bot-13.0.zip
		cd  python-telegram-bot-13.0/
			python3 setup.py install
		cd ..
		rm -rf python-telegram-bot-13.0/
		echo de_DE ISO-8859-1 >>/etc/locale.gen
		echo de_DE.UTF-8 UTF-8 >> /etc/locale.gen
		locale-gen
		echo "Copying files"
		for file in $FILES ; do
			 cp -v $file "$INSTALL_PATH/$file"
		done
		cp -v $SERVICE_FILE	/etc/systemd/system/$SERVICE_FILE
		systemctl deamon-reload
		echo "Starting the service."
		echo "systemctl enable telegram-reminder && systemctl start telegram-reminder"
		systemctl enable telegram-reminder && systemctl start telegram-reminder
		;;
	remove)
		echo "Removing files"
		rm -r -v "$INSTALL_PATH"
		systemctl disable telegram-reminder && systemctl stop telegram-reminder
		rm -v /etc/systemd/system/$SERVICE_FILE
		systemctl deamon-reload
		python3 -m pip remove telegram-bot
		;;
	*)
	echo "Usage is install or remove"
	;;
	
esac

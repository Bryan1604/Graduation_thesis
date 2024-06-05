DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -e
mkdir -p build
if [ ! -d "$DIR/build/apache-rat-0.15" ]; then
	curl -LSs https://dlcdn.apache.org/creadur/apache-rat-0.15/apache-rat-0.15-bin.tar.gz -o "$DIR/build/apache-rat.tar.gz"
	cd $DIR/build
	tar zvxf apache-rat.tar.gz
	cd -
fi
java -jar $DIR/build/apache-rat-0.15/apache-rat-0.15.jar $DIR -e public -e apache-rat-0.15 -e .git -e .gitignore
docker build -t apache/hadoop:3 .
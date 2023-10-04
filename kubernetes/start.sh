docker build -t consumer:v0.0.1 -f consumer/Dockerfile . && \
echo "Made consumer image"

docker build -t producer:v0.0.1 -f producer/Dockerfile . && \
echo "Made producer image"

docker build -t database:v0.0.1 -f database/Dockerfile . && \
echo "Made database image"

kubectl apply -f kafka/namespace.yaml && \
kubectl apply -f kafka/kafka.yaml && \
kubectl apply -f kafka/zookeeper.yaml && \
kubectl apply -f database/database.yaml && \
kubectl apply -f consumer/consumer.yaml && \
kubectl apply -f producer/producer.yaml

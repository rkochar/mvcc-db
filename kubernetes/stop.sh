kubectl delete -f consumer/consumer.yaml && \
kubectl delete -f producer/producer.yaml && \
kubectl delete -f database/database.yaml && \
kubectl delete -f kafka/kafka.yaml && \
kubectl delete -f kafka/zookeeper.yaml && \
kubectl delete -f kafka/namespace.yaml

gcloud iam service-accounts create k8s-deployer \
    --display-name="Kubernetes Deployer" \
    --project=sa-project-482311

gcloud projects add-iam-policy-binding sa-project-482311 \
    --member="serviceAccount:k8s-deployer@sa-project-482311.iam.gserviceaccount.com" \
    --role="roles/container.developer

gcloud projects add-iam-policy-binding sa-project-482311 \
    --member="serviceAccount:k8s-deployer@sa-project-482311.iam.gserviceaccount.com" \
    --role="roles/container.clusterAdmin"

gcloud iam service-accounts keys create gcp-key.json \
    --iam-account=k8s-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com
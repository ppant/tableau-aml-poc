import os
from azure.ai.ml import Input, MLClient, load_job
from azure.identity import DefaultAzureCredential


def get_ml_client() -> MLClient:
    return MLClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ["AZ_SUBSCRIPTION_ID"],
        resource_group_name=os.environ["AZ_RESOURCE_GROUP"],
        workspace_name=os.environ["AZ_ML_WORKSPACE"],
    )


def submit_pipeline_job(input_blob_url: str) -> tuple[str, str]:
    ml_client = get_ml_client()

    pipeline_job = load_job(source=os.environ.get("PIPELINE_JOB_YAML", "aml/pipeline_job.yml"))
    pipeline_job.inputs["input_data"] = Input(type="uri_file", path=input_blob_url)

    submitted_job = ml_client.jobs.create_or_update(pipeline_job)

    studio_base = (
        "https://ml.azure.com/runs/{job}?wsid=/subscriptions/{sub}/resourcegroups/{rg}/providers/Microsoft.MachineLearningServices/workspaces/{ws}"
    )
    studio_url = studio_base.format(
        job=submitted_job.name,
        sub=os.environ["AZ_SUBSCRIPTION_ID"],
        rg=os.environ["AZ_RESOURCE_GROUP"],
        ws=os.environ["AZ_ML_WORKSPACE"],
    )
    return submitted_job.name, studio_url

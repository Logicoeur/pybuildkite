from pybuildkite.client import Client


class Pipelines(Client):
    """
    Pipeline operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client:
        :param base_url:
        """
        self.client = client
        self.path = base_url + "organizations/{}/pipelines/"

    def list_pipelines(self, organization, page=0, with_pagination=False):
        """
        Returns a paginated list of an organization’s pipelines.

        :param organization: Organization slug
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a paginated list of an organization’s pipelines.
        """
        query_params = {"page": page}
        return self.client.get(
            self.path.format(organization),
            query_params=query_params,
            with_pagination=with_pagination,
        )

    def get_pipeline(self, organization, pipeline_name):
        """
        Get a pipeline

        :param organization: Organization slug
        :param pipeline_name: Pipeline slug
        :return: A pipeline
        """
        return self.client.get(self.path.format(organization) + pipeline_name)

    def create_pipeline(
        self,
        organization,
        pipeline_name,
        git_repository,
        build_steps=[
            dict(
                type="script",
                name=":pipeline:",
                command="buildkite-agent pipeline upload",
            )
        ],
    ):
        """
        Create a pipeline
        :param build_steps: list of build pipeline steps
        Command: { "type": "script", "name": "Script", "command": "command.sh" }
        Wait for all previous steps to finish: { "type": "waiter" }
        Block pipeline (see the job unblock API): { "type": "manual" }
        Trigger pipeline: { "type": "trigger", "trigger_project_slug": "a-pipeline" }
        :param organization: Organization slug
        :param pipeline_name:Pipeline slug
        :param git_repository: repo URL
        :return:
        """
        data = {
            "name": pipeline_name,
            "repository": git_repository,
            "steps": build_steps,
        }

        return self.client.post(self.path.format(organization), body=data)

    def delete_pipeline(self, organization, pipeline):
        """
        Delete a pipeline
        :param organization: Organization slug
        :param pipeline:Pipeline slug
        :return:
        """
        url = self.path.format(organization) + pipeline
        return self.client.delete(url)

    def update_pipeline(self, organization, pipeline):
        """
        """
        body = {
            "description": "'CI Pipeline for the PyBuildkite wrapper"
        }
        url = self.path.format(organization) + pipeline
        return self.client.patch(url, body=body)
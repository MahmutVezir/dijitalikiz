"""Independent ECR list_images reproducer for getmoto/moto#8269."""
from __future__ import annotations

import json
import unittest

import boto3
from moto import mock_aws


def make_manifest() -> dict:
    return {
        "schemaVersion": 2,
        "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
        "config": {
            "mediaType": "application/vnd.docker.container.image.v1+json",
            "size": 1,
            "digest": "sha256:" + "a" * 64,
        },
        "layers": [
            {
                "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                "size": 1,
                "digest": "sha256:" + "b" * 64,
            }
        ],
    }


class MotoIssue8269Regression(unittest.TestCase):
    @mock_aws
    def test_list_images_returns_each_tag_for_one_image_digest(self) -> None:
        client = boto3.client("ecr", region_name="us-east-1")
        client.create_repository(repositoryName="reponame")
        manifest = json.dumps(make_manifest())

        client.put_image(
            repositoryName="reponame",
            imageTag="tag1",
            imageManifest=manifest,
        )
        client.put_image(
            repositoryName="reponame",
            imageTag="tag2",
            imageManifest=manifest,
        )

        images = client.list_images(repositoryName="reponame")["imageIds"]
        self.assertEqual(len(images), 2)
        self.assertEqual(
            {image["imageTag"] for image in images},
            {"tag1", "tag2"},
        )
        self.assertEqual(images[0]["imageDigest"], images[1]["imageDigest"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

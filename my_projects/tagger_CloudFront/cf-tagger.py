from importlib.resources import Resource
import boto3
from importlib_metadata import distribution
from yaml import BlockMappingStartToken


class CloudFrontWrapper:
    """Encapsulates Amazon CloudFront operations."""

    def __init__(self, cloudfront_client):
        """
        :param cloudfront_client: A Boto3 CloudFront client
        """
        self.cloudfront_client = cloudfront_client

    def list_distributions(self):
        print("CloudFront distributions:\n")
        tagged_dist = []
        distributions = self.cloudfront_client.list_distributions()
        if distributions["DistributionList"]["Quantity"] > 0:
            for distribution in distributions["DistributionList"]["Items"]:
                # print(distribution)
                print(f"Domain: {distribution['DomainName']}")
                print(f"Distribution Id: {distribution['Id']}")
                print(
                    f"Certificate Source: "
                    f"{distribution['ViewerCertificate']['CertificateSource']}"
                )
                if distribution["ViewerCertificate"]["CertificateSource"] == "acm":
                    print(
                        f"Certificate: {distribution['ViewerCertificate']['Certificate']}"
                    )
                if distribution["Aliases"]["Quantity"] > 0:
                    for alias in distribution["Aliases"]["Items"]:
                        print(f"Alias: {alias}")
                    x = alias.split(".")
                    # print('aliasy: ', x)
                    reg_list = ("eu1", "cn1", "ap1", "eu2")
                    eu_list = ["eu1", "www"]
                    while alias == "x.y.z":
                        reg = "eu1"
                        break
                    for elem in x:
                        if elem in eu_list:
                            reg = "eu1"
                        for elem1 in reg_list:
                            if elem == elem1:
                                reg = elem1

                    env_list = (
                        "devops",
                        "dev",
                        "test",
                        "uat",
                        "pre",
                        "prod",
                        "migration",
                    )
                    dev_list = ["dev", "cicd"]
                    prod_list = ["prod", "ep"]
                    for elem2 in x:
                        if elem2 in dev_list:
                            envi = "dev"
                            break
                        if elem2 in prod_list:
                            envi = "prod"
                            break
                        for elem3 in env_list:
                            if elem2 == elem3:
                                envi = elem3
                    tags = {"designatedRegion": reg, "environmentName": envi}
                    # tags['environmentName']= envi
                    # print(f"Tags: {tags}")
                    formated_tags = [{"Key": k, "Value": v} for k, v in tags.items()]
                    tagged_distro = {
                        "ARN": distribution["ARN"],
                        "Tags": formated_tags,
                        "Alias": alias,
                    }
                    tagged_dist.append(tagged_distro)
                # print("")
            return tagged_dist
        else:
            print("No CloudFront distributions detected.")

    def update_distributions(self, tags):
        for distro_tags in tags:
            self.cloudfront_client.tag_resource(
                Resource=distro_tags["ARN"], Tags={"Items": distro_tags["Tags"]}
            )
            print(distro_tags)

        # function input: domain name, output: tags


def main():
    cloudfront = CloudFrontWrapper(boto3.client("cloudfront"))
    y = cloudfront.list_distributions()
    cloudfront.update_distributions(y)

    # print(*y, sep='\n')


if __name__ == "__main__":
    main()

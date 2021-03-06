import subprocess

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.gluster_integration.objects.volume import Volume


class Create(objects.BaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(Create, self).__init__(*args, **kwargs)

    def run(self):
        args = {}
        if self.parameters.get('Volume.replica_count') is not None:
            args.update({
                "replica_count": self.parameters.get('Volume.replica_count')
            })
        if self.parameters.get('Volume.transport') is not None:
            args.update({
                "transport": self.parameters.get('Volume.transport')
            })
        if self.parameters.get('Volume.disperse_count') is not None:
            args.update({
                "disperse_count": self.parameters.get('Volume.disperse_count')
            })
        if self.parameters.get('Volume.redundancy_count') is not None:
            args.update({
                "redundancy_count": self.parameters.get(
                    'Volume.redundancy_count'
                )
            })
        if self.parameters.get('Volume.tuned_profile') is not None:
            args.update({
                "tuned_profile": self.parameters.get('Volume.tuned_profile')
            })
        if self.parameters.get('Volume.force') is not None:
            args.update({
                "force": self.parameters.get('Volume.force')
            })

        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Creating the volume %s" %
                    self.parameters['Volume.volname']
                },
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        if NS.gdeploy_plugin.create_volume(
                self.parameters.get('Volume.volname'),
                self.parameters.get('Volume.bricks'),
                **args
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Created the volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
        else:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Volume creation failed for volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False
        if NS.gdeploy_plugin.start_volume(
                self.parameters.get('Volume.volname'),
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Started the volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
        else:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Failed to start the volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False
        return True

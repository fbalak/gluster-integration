from tendrl.commons import flows
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class CreateGlusterBrick(flows.BaseFlow):
    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Starting Brick creation flow"
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        super(CreateGlusterBrick, self).run()

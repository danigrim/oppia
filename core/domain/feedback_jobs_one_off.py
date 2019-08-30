# Copyright 2019 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""One-off jobs for feedback models."""
from __future__ import absolute_import # pylint: disable=import-only-modules

from core import jobs
from core.platform import models

(feedback_models,) = models.Registry.import_models([models.NAMES.feedback])


class GeneralFeedbackThreadUserOneOffJob(jobs.BaseMapReduceOneOffJobManager):
    """One-off job for setting user_id and thread_id for all
     GeneralFeedbackThreadUserModels.
    """
    @classmethod
    def entity_classes_to_map_over(cls):
        """Return a list of datastore class references to map over."""
        return [feedback_models.GeneralFeedbackThreadUserModel]

    @staticmethod
    def map(model_instance):
        """Implements the map function for this job."""
        user_id, thread_id = model_instance.id.split('.', 1)
        if model_instance.user_id is None:
            model_instance.user_id = user_id
        if model_instance.thread_id is None:
            model_instance.thread_id = thread_id
        model_instance.put(update_last_updated_time=False)
        yield ('SUCCESS', model_instance.id)

    @staticmethod
    def reduce(key, values):
        yield (key, len(values))

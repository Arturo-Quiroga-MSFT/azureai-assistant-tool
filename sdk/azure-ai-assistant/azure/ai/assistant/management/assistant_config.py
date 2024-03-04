# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

import json
from azure.ai.assistant.management.function_config import FunctionConfig
from azure.ai.assistant.management.logger_module import logger
import os


class AssistantConfig:
    """
    A class representing the configuration for an assistant.

    :param name: The name of the assistant.
    :type name: str
    :param config_data: The configuration data for the assistant.
    :type config_data: dict
    """
    def __init__(self, 
                 name : str,
                 config_data : dict
    ) -> None:
        self._name = name
        self._config_data = config_data
        self._instructions = config_data['instructions']
        if 'assistant_id' not in config_data:
            logger.info("assistant_id not found in config. Setting assistant_id to None.")
            self._assistant_id = None
        else:
            self._assistant_id = config_data['assistant_id'] if config_data['assistant_id'] != "" else None
        self._ai_client_type = config_data['ai_client_type'] if 'ai_client_type' in config_data else "OPEN_AI"
        self._model = config_data['model']
        # Process the knowledge_files to replace empty strings with None
        raw_knowledge_files = config_data.get('knowledge_files', {})
        self._knowledge_files = {k: (v if v != '' else None) for k, v in raw_knowledge_files.items()}
        self._selected_functions = config_data.get('selected_functions', [])
        self._function_configs = self._get_function_configs()
        # enable knowledge retrieval when set to True in config
        self._knowledge_retrieval = config_data.get('knowledge_retrieval', False)
        # enable code_interpreter when set to True in config
        self._code_interpreter = config_data.get('code_interpreter', False)
        # set default output folder as absolute path to 'output' folder in current directory
        default_output_folder_path = os.path.join(os.getcwd(), 'output')
        self._output_folder_path = config_data.get('output_folder_path', default_output_folder_path)
        self._assistant_type = config_data.get('assistant_type', 'assistant')

    def __eq__(self, other):
        if not isinstance(other, AssistantConfig):
            return NotImplemented

        return (self._name == other._name and
                self._instructions == other._instructions and
                self._assistant_id == other._assistant_id and
                self._ai_client_type == other._ai_client_type and
                self._model == other._model and
                self._knowledge_files == other._knowledge_files and
                self._selected_functions == other._selected_functions and
                self._knowledge_retrieval == other._knowledge_retrieval and
                self._code_interpreter == other._code_interpreter)

    @classmethod
    def from_dict(
        self, 
        config_data : dict
    ) -> 'AssistantConfig':
        """
        Create an AssistantConfig object from a dictionary.

        :param config_data: The configuration data for the assistant.
        :type config_data: dict

        :return: The AssistantConfig object.
        :rtype: AssistantConfig
        """
        return AssistantConfig(config_data['name'], config_data)

    def to_json(self) -> str:
        """Return the configuration data as a JSON string.
        
        :return: The configuration data as a JSON string.
        :rtype: str
        """
        return json.dumps(self._get_config_data(), indent=4)

    def _get_config_data(self):
        self._config_data['name'] = self._name
        self._config_data['instructions'] = self._instructions
        self._config_data['assistant_id'] = self._assistant_id
        self._config_data['ai_client_type'] = self._ai_client_type
        self._config_data['model'] = self._model
        self._config_data['knowledge_files'] = self._knowledge_files
        self._config_data['knowledge_retrieval'] = self._knowledge_retrieval
        self._config_data['code_interpreter'] = self._code_interpreter
        self._config_data['selected_functions'] = self._selected_functions
        self._config_data['output_folder_path'] = self._output_folder_path
        return self._config_data

    def _get_function_configs(self):
        function_configs = []
        for function_spec in self._selected_functions:
            function_configs.append(FunctionConfig(function_spec))
        return function_configs
    
    @property
    def name(self) -> str:
        """Get the name.
        
        :return: The name of the assistant.
        :rtype: str
        """
        return self._name

    @property
    def assistant_id(self) -> str:
        """Get the assistant ID.
        
        :return: The assistant ID.
        :rtype: str
        """
        return self._assistant_id

    @assistant_id.setter
    def assistant_id(self, value) -> None:
        """
        Set the assistant ID.
        
        :param value: The assistant ID.
        :type value: str
        """
        self._assistant_id = value

    @property
    def ai_client_type(self) -> str:
        """Get the AI client type.
        
        :return: The AI client type.
        :rtype: str
        """
        return self._ai_client_type
    
    @property
    def model(self) -> str:
        """Get the model.
        
        :return: The model.
        :rtype: str
        """
        return self._model
    
    @model.setter
    def model(self, value) -> None:
        """
        Set the model.
        
        :param value: The model.
        :type value: str
        """
        self._model = value

    @property
    def knowledge_files(self) -> dict:
        """Get the knowledge files.
        
        :return: The knowledge files.
        :rtype: dict
        """
        return self._knowledge_files
    
    @knowledge_files.setter
    def knowledge_files(self, value) -> None:
        """
        Set the knowledge files.
        
        :param value: The knowledge files.
        :type value: dict
        """
        self._knowledge_files = value

    @property
    def knowledge_retrieval(self) -> bool:
        """Get the knowledge retrieval.
        
        :return: The knowledge retrieval.
        :rtype: bool
        """
        return self._knowledge_retrieval

    @knowledge_retrieval.setter
    def knowledge_retrieval(self, value) -> None:
        """
        Set the knowledge retrieval.
        
        :param value: The knowledge retrieval.
        :type value: bool
        """
        self._knowledge_retrieval = value

    @property
    def code_interpreter(self) -> bool:
        """Get the code interpreter.
        
        :return: The code interpreter.
        :rtype: bool
        """
        return self._code_interpreter
    
    @code_interpreter.setter
    def code_interpreter(self, value) -> None:
        """
        Set the code interpreter.
        
        :param value: The code interpreter.
        :type value: bool
        """
        self._code_interpreter = value

    @property
    def selected_functions(self) -> list:
        """Get the selected functions.
        
        :return: The selected functions.
        :rtype: list
        """
        return self._selected_functions
    
    @selected_functions.setter
    def selected_functions(self, value) -> None:
        """
        Set the selected functions.
        
        :param value: The selected functions.
        :type value: list
        """
        self._selected_functions = value

    @property
    def instructions(self) -> str:
        """Get the instructions.
        
        :return: The instructions.
        :rtype: str
        """
        return self._instructions
    
    @instructions.setter
    def instructions(self, value) -> None:
        """
        Set the instructions.
        
        :param value: The instructions.
        :type value: str
        """
        self._instructions = value

    @property
    def output_folder_path(self) -> str:
        """Get the output folder path.
        
        :return: The output folder path.
        :rtype: str
        """
        return self._output_folder_path
    
    @output_folder_path.setter
    def output_folder_path(self, value) -> None:
        """
        Set the output folder path.
        
        :param value: The output folder path.
        :type value: str
        """
        self._output_folder_path = value

    @property
    def assistant_type(self) -> str:
        """Get the assistant type.
        
        :return: The assistant type.
        :rtype: str
        """
        return self._assistant_type

from typing import Any, Literal, Sequence
from geomeppyupdated.idf import IDF
from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass
from utils4plans.lists import get_unique_one

from plan2eplus.errors import InvalidObjectError, NonExistentEpBunchTypeError

Identifiers = Literal["Name", "Surface_Name"]


def get_object_description(object: EpBunch):
    d = {k: v for k, v in zip(object.fieldnames, object.fieldvalues)}
    d.pop("key")
    # TODO: not sure how safe this is..
    if "Polygon" in d.keys():
        d.pop("Polygon")
    return d


def filter_relevant_values(existing_values: dict, relevant_values: dict):
    return {k: v for k, v in existing_values.items() if k in relevant_values.keys()}


@dataclass
class IDFObject:
    @property
    def key(self) -> str: ...

    @property
    def values(self):
        return self.__dict__

    @classmethod
    def read(cls, idf: IDF, *args, **kwargs):
        objects = idf.idfobjects[cls().key]

        return [cls(**get_object_description(i)) for i in objects]

    @classmethod
    def read_and_filter(cls, idf: IDF, *args, **kwargs):
        objects = idf.idfobjects[cls().key]

        def filter_d(d: dict):
            return {k: v for k, v in d.items() if k in cls().values.keys()}

        return [cls(**filter_d(get_object_description(i))) for i in objects]

    @classmethod
    def read_by_name(cls, idf: IDF, names: list[str] = []):
        objects = idf.idfobjects[cls().key]
        if names:
            return [
                cls(**get_object_description(i)) for i in objects if i.Name in names
            ]
        return [cls(**get_object_description(i)) for i in objects]

    @classmethod
    def read_one_by_name(cls, idf: IDF, name: str):
        res = cls.read(idf, [name])
        assert len(res) == 1, f"Expected to get only one item, insted got {res}"
        return res[0]

    def get_idf_objects(self, idf: IDF) -> list[EpBunch]:
        return idf.idfobjects[self.key]

    def get_one_idf_object(
        self, idf: IDF, name: str, identifier_name: Identifiers = "Name"
    ) -> EpBunch:
        objects = self.get_idf_objects(idf)
        if not objects:
            raise NonExistentEpBunchTypeError(f"No objects with key {self.key} in IDF")

        check_has_identifier(objects[0], identifier_name)
        try:
            object = get_unique_one(
                objects,
                lambda x: x[identifier_name] == name,
            )
        except AssertionError:
            raise InvalidObjectError(self, name, identifier_name)
        return object

    def update(
        self,
        idf: IDF,
        object_name: str,
        param: str,
        new_value: str,
        identifier: Identifiers = "Name",
    ):
        object = self.get_one_idf_object(idf, object_name, identifier)
        # TODO are fieldnames a better fit here?
        keys = list(self.values.keys())
        assert (
            param in keys
        ), f"{param} does not exist in {keys} for object named '{object_name} with type {type(self)}"
        object[param] = new_value

    def write(self, idf: IDF):
        idf.newidfobject(self.key, **self.values)
        return idf

    def overwrite(self, idf: IDF):
        existing_idf_objects = idf.idfobjects[self.key]
        for o in existing_idf_objects:
            idf.removeidfobject(o)
        self.write(idf)

    def create_ezobject(self, *args, **kwargs) -> Any: ...


def check_has_identifier(obj: EpBunch, param_name: Identifiers):
    assert (
        param_name in obj.fieldnames
    ), f"No attribute of {param_name} for epbunch with key {obj.key}"
    return True


def get_names_of_idf_objects(objects: Sequence[IDFObject]):
    lst: list[str] = []
    for o in objects:
        try:
            name: str = o.__getattribute__("Name")
            lst.append(name)
        except AttributeError:
            f"No attribute Name for objects of type(s): {set([type(i) for i in objects])}"
    return lst

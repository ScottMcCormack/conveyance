.. _api:

Developer Interface
===================

.. module:: conveyance

Conveyance
----------

.. autoclass:: conveyance.conveyance.Conveyance


Belt Capacity
-------------

.. autofunction:: conveyance.belt_capacity.mass_density_material
.. autofunction:: conveyance.belt_capacity.mass_density_idler
.. autofunction:: conveyance.belt_capacity.volume_carried_material
.. autofunction:: conveyance.belt_capacity.volumetric_flow
.. autofunction:: conveyance.belt_capacity.belt_cs_area

Conveyor Resistances
--------------------

.. autofunction:: conveyance.conveyor_resistances.resistance_main
.. autofunction:: conveyance.conveyor_resistances.resistance_secondary
.. autofunction:: conveyance.conveyor_resistances.resistance_concentrated
.. autofunction:: conveyance.conveyor_resistances.resistance_gravity
.. autofunction:: conveyance.conveyor_resistances.resistance_inertial_friction
.. autofunction:: conveyance.conveyor_resistances.resistance_material_acceleration
.. autofunction:: conveyance.conveyor_resistances.resistance_belt_wrap
.. autofunction:: conveyance.conveyor_resistances.resistance_material_skirtplates
.. autofunction:: conveyance.conveyor_resistances.resistance_belt_cleaners
.. autofunction:: conveyance.conveyor_resistances.resistance_belt_sag_tension
.. autofunction:: conveyance.conveyor_resistances.resistance_belt_wrap_iso
.. autofunction:: conveyance.conveyor_resistances.tension_transmit_min

Power Requirements
------------------

.. autofunction:: conveyance.power_requirements.power_requirements_motor

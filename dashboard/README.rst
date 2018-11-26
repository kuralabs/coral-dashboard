
RESTful API
===========

Pushing data to the UI:

.. code-block:: sh

    curl http://localhost:5000/api/push \
       --request POST \
       --header "Content-Type: application/json" \
       --data '{"data": {"temp_coolant": {"percent": 70.0, "value": null, "total": null}}}'

Accesing server logs:

.. code-block:: sh

   curl http://localhost:5000/api/logs

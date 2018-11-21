
RESTful API
===========

Pushing data to the UI:

.. code-block:: sh

    curl http://localhost:5000/api/push \
       --request POST \
       --header "Content-Type: application/json" \
       --data '{"header": "Testing...", "bargraph": 10}'

Accesing server logs:

.. code-block:: sh

   curl http://localhost:5000/api/logs

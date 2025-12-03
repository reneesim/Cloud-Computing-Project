Ticket Purchase API
```
openapi: 3.1.0
info:
  title: Ticket Purchase API
  version: 1.0.0
  description: API for browsing ticket types and purchasing tickets.

servers:
  - url: https://129.192.69.172:5000/v1

paths:
  /tickets:
    get:
      summary: Get available ticket types
      parameters:
        - in: query
          name: type
          schema:
            type: string
          description: Filter by ticket type
        - in: query
          name: min_price
          schema:
            type: number
          description: Minimum price filter
        - in: query
          name: max_price
          schema:
            type: number
          description: Maximum price filter
      responses:
        "200":
          description: List of available tickets
          content:
            application/json:
              schema:
                type: object
                properties:
                  tickets:
                    type: array
                    items:
                      $ref: "#/components/schemas/Ticket"

  /orders/{orderId}:
    get:
      summary: Get order details by ID
      parameters:
        - in: path
          name: orderId
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Order details
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Order"
        "404":
          description: Order not found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /orders:
    post:
      summary: Create a new ticket order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateOrderRequest"
      responses:
        "201":
          description: Order successfully created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CreateOrderResponse"
        "400":
          description: Invalid request body
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

components:
  schemas:

    Ticket:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        type:
          type: string
          example: "adult"
        price:
          type: number
          example: 25.00
        currency:
          type: string
          example: "USD"
        description:
          type: string

    OrderItem:
      type: object
      properties:
        ticketId:
          type: string
        type:
          type: string
        qty:
          type: integer
        unitPrice:
          type: number
        total:
          type: number

    Order:
      type: object
      properties:
        orderId:
          type: string
        customer:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
        items:
          type: array
          items:
            $ref: "#/components/schemas/OrderItem"
        grandTotal:
          type: number
        currency:
          type: string
        status:
          type: string
          example: "confirmed"
        createdAt:
          type: string
          format: date-time

    CreateOrderRequest:
      type: object
      required:
        - customer
        - items
        - paymentMethod
      properties:
        customer:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
        items:
          type: array
          items:
            type: object
            required:
              - ticketId
              - qty
            properties:
              ticketId:
                type: string
              qty:
                type: integer
        paymentMethod:
          type: string
          example: "credit_card"

    CreateOrderResponse:
      type: object
      properties:
        orderId:
          type: string
        status:
          type: string
        grandTotal:
          type: number
        currency:
          type: string
        message:
          type: string

    Error:
      type: object
      properties:
        error:
          type: string

```


Database API
```
openapi: 3.1.0
info:
  title: Redis CRUD API
  version: 1.0.0
  description: REST API wrapper for CRUD operations on a Redis key-value store.

servers:
  - url: https://129.192.69.172:6379/v1

paths:
  /redis:
    post:
      summary: Create a new Redis key-value entry
      description: Creates a new key with a JSON value in Redis.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateRedisEntry"
      responses:
        "201":
          description: Successfully created key
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SuccessMessage"
        "400":
          description: Invalid request body
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /redis/{key}:
    get:
      summary: Read a Redis key-value entry
      description: Retrieves a value stored at the given key.
      parameters:
        - in: path
          name: key
          schema:
            type: string
          required: true
      responses:
        "200":
          description: Redis key value fetched successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/RedisEntry"
        "404":
          description: Key not found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

    put:
      summary: Update an existing Redis key
      description: Replaces the value at an existing Redis key.
      parameters:
        - in: path
          name: key
          schema:
            type: string
          required: true
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpdateRedisEntry"
      responses:
        "200":
          description: Key updated successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SuccessMessage"
        "404":
          description: Key not found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

    delete:
      summary: Delete a Redis key
      description: Removes a key from Redis.
      parameters:
        - in: path
          name: key
          schema:
            type: string
          required: true
      responses:
        "200":
          description: Key deleted successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SuccessMessage"
        "404":
          description: Key not found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

components:
  schemas:

    CreateRedisEntry:
      type: object
      required:
        - key
        - value
      properties:
        key:
          type: string
          example: "user:1001"
        value:
          type: object
          description: JSON object to store at the key
          example:
            name: "Alice"
            age: 25
            role: "admin"

    UpdateRedisEntry:
      type: object
      required:
        - value
      properties:
        value:
          type: object
          description: JSON value to overwrite the existing key
          example:
            name: "Alice Anderson"
            age: 26
            role: "admin"

    RedisEntry:
      type: object
      properties:
        key:
          type: string
          example: "user:1001"
        value:
          type: object
          example:
            name: "Alice"
            age: 25
            role: "admin"

    SuccessMessage:
      type: object
      properties:
        message:
          type: string
          example: "Operation completed successfully"
        key:
          type: string
          example: "user:1001"

    Error:
      type: object
      properties:
        error:
          type: string
          example: "Key not found"
```

from app.application.dto.product_dto import CreateProductRequest, ProductResponse
from app.domain.entities.product import Product


class ProductMapper:

    @staticmethod
    def request_to_entity(request: CreateProductRequest) -> Product:
        return Product(
            id=None,
            name=request.name,
            code=request.code,
            description=request.description,
            price=request.price,
            current_stock=request.current_stock,
            minimum_stock=request.minimum_stock,
        )

    @staticmethod
    def entity_to_response(product: Product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name,
            code=product.code,
            description=product.description,
            price=product.price,
            current_stock=product.current_stock,
            minimum_stock=product.minimum_stock,
            is_active=product.is_active,
        )
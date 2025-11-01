"""gRPC server implementation for currency conversion service."""

import grpc
from concurrent import futures
import sys
import os

# Import generated proto modules
# These are generated in Dockerfile using: python -m grpc_tools.protoc -I proto --python_out=app --grpc_python_out=app proto/currency.proto
try:
    import currency_pb2
    import currency_pb2_grpc
except ImportError:
    print("Error: Proto files not generated. Run:")
    print("python -m grpc_tools.protoc -I proto --python_out=app --grpc_python_out=app proto/currency.proto")
    sys.exit(1)

from currency_service import convert_currency


class CurrencyService(currency_pb2_grpc.CurrencyServiceServicer):
    """gRPC service implementation for currency conversion."""
    
    def Convert(self, request, context):
        """
        Convert currency from one to another.
        
        Args:
            request: ConvertRequest with from_currency, to_currency, and amount
            context: gRPC context
        
        Returns:
            ConvertResponse with converted_amount, rate, and message
        """
        try:
            result = convert_currency(
                from_currency=request.from_currency,
                to_currency=request.to_currency,
                amount=request.amount
            )
            
            return currency_pb2.ConvertResponse(
                converted_amount=result['converted_amount'],
                rate=result['rate'],
                message=result['message']
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error converting currency: {str(e)}')
            return currency_pb2.ConvertResponse(
                converted_amount=0.0,
                rate=0.0,
                message=f'Error: {str(e)}'
            )


def serve():
    """Start the gRPC server."""
    port = os.getenv('GRPC_PORT', '50051')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    currency_pb2_grpc.add_CurrencyServiceServicer_to_server(
        CurrencyService(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'gRPC server started on port {port}')
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        server.stop(0)


if __name__ == '__main__':
    serve()


import { Injectable, OnModuleInit } from '@nestjs/common';
import { Client, Transport } from '@nestjs/microservices';
import type { ClientGrpc } from '@nestjs/microservices';
import { join } from 'path';
import { firstValueFrom } from 'rxjs';

interface CurrencyService {
  Convert(data: { from_currency: string; to_currency: string; amount: number }): any;
}

@Injectable()
export class AppService implements OnModuleInit {
  @Client({
    transport: Transport.GRPC,
    options: {
      package: 'currency',
      protoPath: join(__dirname, 'proto/currency.proto'),
      url: process.env.GRPC_SERVER_URL || 'localhost:50051',
    },
  })
  private client: ClientGrpc;

  private currencyService: CurrencyService;

  onModuleInit() {
    this.currencyService = this.client.getService<CurrencyService>('CurrencyService');
  }

  async convertCurrency(from: string, to: string, amount: number) {
    const result = this.currencyService.Convert({ from_currency: from, to_currency: to, amount });
    // Convert Observable to Promise if needed
    return firstValueFrom(result);
  }
}

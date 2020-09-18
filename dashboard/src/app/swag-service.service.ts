import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

const APIURL = "http://localhost/"

@Injectable({
  providedIn: 'root'
})
export class SwagServiceService {

  constructor(private http: HttpClient) { }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
        console.error('An error occurred:', error.error.message);
    } else {
        console.error(
            `Backend returned code ${error.status}, ` +
            `body was: ${error.error.error}`);
    }
    return of("");
};

  getItems(): Observable<String[]> {
    return this.http.get<Array<String>>(APIURL + 'items');
  }

  getObjectList(name): Observable<String[]> {
    return this.http.get<Array<String>>(APIURL + "objects?name=" + name);
  }

  getObjectDetails(name, id): Observable<String> {
    return this.http.get<any>(APIURL + "object_details?name=" + name + "&id=" + id).pipe(catchError(this.handleError));
  }

  getLogs(name): Observable<String[]> {
    return this.http.get<Array<String>>(APIURL + "logs?name=" + name);
  }
}

import { Component, OnInit, Input, SimpleChanges, OnChanges, ViewChild } from '@angular/core';

import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { SwagObject } from '../swag-object';

@Component({
  selector: 'app-swag-table',
  templateUrl: './swag-table.component.html',
  styleUrls: ['./swag-table.component.css']
})
export class SwagTableComponent implements OnInit {

  @Input()
  objects: [];

  @Input()
  name: String;

  @Input()
  isLoading: Boolean;

  apiUrl = "http://localhost/"
  displayedColumns: string[] = ['objectId', 'label', "precision", "direction", "image_path", "first_appear", "last_appear", "avg_speed"];
  dataSource: MatTableDataSource<SwagObject>;
  resultsLength = 0;

  @ViewChild(MatPaginator, { static: false }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: false }) sort: MatSort;

  constructor() { }

  ngOnInit(): void {
    this.dataSource = new MatTableDataSource(new Array<SwagObject>());
    
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['isLoading'] && changes['isLoading'].currentValue == false) {
      this.refreshDataSource();
    }
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  refreshDataSource() {
    this.dataSource = new MatTableDataSource(this.objects);
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
    this.resultsLength = this.objects.length;
  }

}

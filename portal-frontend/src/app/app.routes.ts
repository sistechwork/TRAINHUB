import { Routes } from '@angular/router';
import { LoginComponent } from './login/login';
import { DetailsComponent } from './details/details.component';
import { HrmComponent } from './hrm/hrm.component';
import { Learning } from './learning/learning';
import { Project } from './project/project';
import { Setting } from './setting/setting';
import { Validation } from './validation/validation';
import { AdminDashboard } from './admin-dashboard/admin-dashboard';
import { AdminStudentEdit } from './admin-student-edit/admin-student-edit';
import { Signup } from './signup/signup';

export const routes: Routes = [
    { path: 'details', component: DetailsComponent },
    { path: 'hrm', component: HrmComponent },
    { path: 'learning', component: Learning },
    { path: 'project', component: Project },
    { path: 'setting', component: Setting },
    { path: 'validation', component: Validation },
    { path: 'admin-dashboard', component: AdminDashboard },
    { path: 'admin-student-edit', component: AdminStudentEdit },
    { path: 'signup', component: Signup },
    { path: '', component: LoginComponent },
    { path: '**', redirectTo: '' }
];

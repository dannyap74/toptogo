//
//  RegisterView.swift
//  CSTutor
//
//  Created by Даниил Палеев on 30.10.2019.
//  Copyright © 2019 Даниил Палеев. All rights reserved.
//

import SwiftUI

struct RegisterView: View {
    @EnvironmentObject var userManager: UserManager
    @ObservedObject var keyboardHandler: KeyboardFollower
    @State var password1: String = ""
    @State var password2: String = ""
    @State var lenAlert: Bool = false
    @State var passAlert: Bool = false
    @State var wrongAlert: Bool = false
    var body: some View {
        VStack{
            VStack{
                TextField("Username", text: $userManager.profile.username).padding(.bottom, 5)
                TextField("E-mail", text: $userManager.profile.email).padding(.bottom, 5)
                TextField("Judge ID (только цифры)", text: $userManager.profile.judge_id).padding(.bottom, 5)
                TextField("Password", text: $password1).padding(.bottom, 5)
                TextField("Password (again)", text: $password2)
            }
            .padding(.leading)
                .font(Font.system(size: 20, design: .default))
            
            HStack {
              Spacer()
            
              Toggle(isOn: $userManager.settings.rememberUser) {
                Text("Remember me")
                  .font(.subheadline)
                  .multilineTextAlignment(.trailing)
                  .foregroundColor(.gray)
              }
            }
            
            Button(action: self.registerUser) {
              HStack {
                Text("Sign in")
                  .font(Font.system(size: 22, design: .default))
                  .bold()
              }
            }.bordered()
            
        }
        .padding(.trailing)
        .alert(isPresented: $lenAlert) {
            Alert(title: Text("Короткий пароль"), message: Text("Пароль должен состоять минимум из 8 символов"))
        }
        .alert(isPresented: $passAlert) {
            Alert(title: Text("Пароли не совпадают"))
        }
        .alert(isPresented: $wrongAlert) {
            Alert(title: Text("Уже есть пользователь с таким логином или e-mail"))
        }
    }
}

// MARK: - Event Handlers
extension RegisterView {
    func registerUser() { 
        if password1.count < 8 {
            lenAlert = true
        }
        else if password1 != password2 {
            passAlert = true
        }
        else{
            userManager.profile.password = password1
            RegistrationAPI(profile: userManager.profile) { (token) in
                if let token = token{
                    print(token)
                    self.userManager.settings.token = token
                }
                else{
                    self.wrongAlert = true
                }
            }
        }
    }
}

#if DEBUG
struct RegisterView_Previews: PreviewProvider {
  static let user = UserManager()

  static var previews: some View {
    RegisterView(keyboardHandler: KeyboardFollower())
      .environmentObject(user)
  }
}
#endif
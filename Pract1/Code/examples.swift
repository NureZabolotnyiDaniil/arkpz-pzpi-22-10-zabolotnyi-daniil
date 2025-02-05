// Стильові рекомендації
// Гарний приклад
func fetchUserProfile(with id: Int) -> UserProfile? {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else { return nil }
    do {
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        return try decoder.decode(UserProfile.self, from: data)
    } catch {
        print("Error: \(error)")
        return nil
    }
}
// Поганий приклад
func fetchUserProfile(with id:Int)->UserProfile?{
guard let url=URL(string:"https://api.example.com/users/\(id)") else{return nil}
do{
let data=try Data (contentsOf:url)
let decoder=JSONDecoder()
return try decoder.decode (UserProfile.self, from:data)
}catch{print("Error:\(error)"); return nil}
}


// Правила іменування
// Гарний приклад
func parseUserResponse(_ response: HTTPURLResponse, data: Data) -> Result<User, Error> {
    guard response.statusCode == 200 else { return .failure(NetworkError.invalidResponse) }

    let decoder = JSONDecoder()
    do {
        let user = try decoder.decode(User.self, from: data)
        return .success(user)
    } catch {
        return .failure(NetworkError.decodingError)
    }
}
// Поганий приклад
func prsrsp(_ resp: HTTPURLResponse, d: Data) -> Result<User, Error> {
    guard resp.statusCode == 200 else { return .failure(NetworkError.invalidResponse) }

    let dcr = JSONDecoder()
    do {
        let usr = try dcr.decode(User.self, from: d)
        return .success(usr)
    } catch {
        return .failure(NetworkError.decodingError)
    }
}


// Структура коду
// Гарний приклад
class ProfileViewController: UIViewController {
    // MARK: - Properties

    private let tableView = UITableView()

    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        configureTableView()
    }
}

// MARK: - UITableViewDataSource
extension ProfileViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        10
    }
}
// Поганий приклад
class ProfileViewController: UIViewController, UITableViewDataSource {
    private let tableView = UITableView()

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.dataSource = self
    }

    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        10
    }

    private func someUnrelatedMethod() { }
}


// Рефакторинг
// Гарний приклад
func processOrder(_ order: Order) {
    validate(order)
    let total = calculateTotal(for: order)
    sendConfirmation(total: total)
}

private func calculateTotal(for order: Order) -> Double {
    order.amount * (1 - calculateDiscount(for: order))
}
// Поганий приклад
func processOrder(_ order: Order) {
    validate(order)
    let discount = order.isVIP ? 0.1 : 0.0
    let total = order.amount * (1 - discount)
    sendConfirmation(total: total)

    if order.isVIP {
        let newDiscount = 0.1
        print("VIP Discount: \(newDiscount)")
    }
}


// Оптимізація продуктивності
// Гарний приклад
class ImageProcessor {
    lazy var ciContext: CIContext = {
        CIContext(options: nil)
    }()
    
    func process(image: UIImage) -> UIImage? {
        guard let ciImage = CIImage(image: image),
              let filter = CIFilter(name: "CISepiaTone") else { return nil }
        filter.setValue(ciImage, forKey: kCIInputImageKey)
        filter.setValue(0.8, forKey: kCIInputIntensityKey)
        guard let outputImage = filter.outputImage,
              let cgImage = ciContext.createCGImage(outputImage, from: outputImage.extent)
        else { return nil }
        return UIImage(cgImage: cgImage)
    }
}
// Поганий приклад
class ImageProcessor {
    func process(image: UIImage) -> UIImage? {
        let context = CIContext(options: nil)
        
        guard let ciImage = CIImage(image: image),
              let filter = CIFilter(name: "CISepiaTone") else { return nil }
        filter.setValue(ciImage, forKey: kCIInputImageKey)
        filter.setValue(0.8, forKey: kCIInputIntensityKey)
        guard let outputImage = filter.outputImage,
              let cgImage = context.createCGImage(outputImage, from: outputImage.extent)
        else { return nil }
        return UIImage(cgImage: cgImage)
    }
}


// Обробка помилок
// Гарний приклад
func fetchUserProfile(with id: Int) -> UserProfile? {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else { return nil }
    do {
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        return try decoder.decode(UserProfile.self, from: data)
    } catch {
        print("Error: \(error)")
        return nil
    }
}
// Поганий приклад
func fetchUserProfile(with id: Int) -> UserProfile? {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else { return nil }
    let data = try! Data(contentsOf: url)
    let decoder = JSONDecoder()
    return try? decoder.decode(UserProfile.self, from: data)
}


// Парадигми програмування
// Гарний приклад
struct User {
    let id: Int
    let name: String
    let isActive: Bool
}

struct UserViewModel {
    let displayName: String
}

func createUserViewModels(from users: [User]) -> [UserViewModel] {
    return users.filter { $0.isActive }
        .map { UserViewModel(displayName: $0.name.capitalized) }
}
// Поганий приклад
struct User {
    let id: Int
    let name: String
    let isActive: Bool
}

struct UserViewModel {
    let displayName: String
}

func createUserViewModels(from users: [User]) -> [UserViewModel] {
    var viewModels = [UserViewModel]()
    for user in users {
        if user.isActive {
            let vm = UserViewModel(displayName: user.name)
            viewModels.append(vm)
        }
    }
    return viewModels
}


// Використання guard
// Гарний приклад
func configureUserProfile(with user: User?) {
    guard let user = user,
          let email = user.email,
          !email.isEmpty
    else {
        print("Невірні дані користувача")
        return
    }
    print("Конфігурація профілю для \(user.name) (\(email))")
}
// Поганий приклад
func configureUserProfile(with user: User?) {
    if let user = user {
        if let email = user.email {
            if !email.isEmpty {
                print("Конфігурація профілю для \(user.name) (\(email))")
            } else {
                print("Невірні дані користувача")
            }
        } else {
            print("Невірні дані користувача")
        }
    } else {
        print("Невірні дані користувача")
    }
}


// Безпечна робота з опціоналами
// Гарний приклад
func getUserDisplayName(for user: User?) -> String {
    guard let user = user, let name = user.name, !name.isEmpty else {
        return "Guest"
    }
    return name.capitalized
}

// Поганий приклад
func getUserDisplayName(for user: User?) -> String {
    let name = user!.name!
    return name.capitalized
}
